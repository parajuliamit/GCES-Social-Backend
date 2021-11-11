from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import *

class RegisterUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 100)

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','email','name']

    def get_name(self,obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','email','name','token']
    
    def get_token(self,obj):
        token = AccessToken.for_user(obj)
        return str(token)

class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyPin
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = Announcement
        fields = '__all__'
    
    def get_user(self,obj):
        user = obj.user.first_name 
        if user == '':
            user = obj.user.email

        return user

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.first_name" )
    class Meta:
        model = Comment
        fields = ["id","user","comment","createdAt"]

class CreateCommentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(CreateCommentSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)
                
    class Meta:
        model = Comment
        fields = '__all__'

class BlogsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.first_name")
    liked = serializers.SerializerMethodField(method_name='check_like')
    
    def check_like(self,obj):
        request = self.context.get("request")
        current_user = request.user
        print(current_user.id)
        if obj.likes.filter(id=current_user.id):
            return True
        else:
            return False

    class Meta:
        model = Blog
        fields =["id","user","title","createdAt","total_likes","comment_count","liked"]


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.first_name")
    comment = CommentSerializer(many=True, source="comment_set.all")
    liked = serializers.SerializerMethodField(method_name='check_like')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(BlogSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)
    
    def check_like(self,obj):
        request = self.context.get("request")
        current_user = request.user
        print(current_user.id)
        if obj.likes.filter(id=current_user.id):
            return True
        else:
            return False
 
    class Meta:
        model = Blog
        fields = ["id","user","title","createdAt","total_likes","comment_count","content","comment","liked"]
    

class SuggestionSerializer(serializers.ModelSerializer):
    is_anonymous = serializers.BooleanField()
    class Meta:
        model = Suggestion
        fields = ["is_anonymous","content"]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name","teacher"]

class RoutineSerializer(serializers.ModelSerializer):
    # subject = SubjectSerializer(many=True, source="subject_set.all")

    subject = serializers.SerializerMethodField()

    def get_subject(self, obj):
        subject = Subject.objects.filter(batch = self.context['batch']).filter(routine = obj).first()
        if subject is None :
            return None
        subject_serializer = SubjectSerializer(subject)
        return subject_serializer.data
    class Meta:
        model = Routine
        fields = ["day","time","subject"]

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

class SubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'

class SubmitAssignmentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(SubmitAssignmentSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)
                
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'

class AssignmentsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.first_name")
    status = serializers.SerializerMethodField(method_name='check_status')
    
    def check_status(self,obj):
        request = self.context.get("request")
        current_user = request.user
        user_assignments = AssignmentSubmission.objects.filter(user = current_user)
        if user_assignments: 
            submitted = user_assignments.filter(assignment = obj)       
            if submitted:
                if submitted.filter(is_approved=None):
                    return 'PENDING'
                else: 
                    if submitted.filter(is_approved = False):
                        return 'REJECTED'
                    else:
                        return 'APPROVED'
        return 'TODO'

    class Meta:
        model = Assignment
        fields =["id","user","title","submissionDate","status"]


class AssignmentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.first_name")
    # submissions = SubmissionsSerializer(many=True, source="assignmentsubmission_set.all")
    submissions = serializers.SerializerMethodField(method_name='get_submissions')
    def get_submissions(self,obj):
        request = self.context.get("request")
        current_user = request.user
        user_assignments = AssignmentSubmission.objects.filter(user = current_user).filter(assignment = obj)   
        return SubmissionsSerializer(user_assignments,many=True).data
 
    class Meta:
        model = Assignment
        fields = ["id","user","title","createdAt","description","file","submissionDate","submissions"]
    

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["title","date"]