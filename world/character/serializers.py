from rest_framework import serializers
from django.contrib.auth.models import User
from character.models import Character, Abilities, PlayerClasses, AbilityEffects, AbilityEnhancements


class CharacterSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Character
        fields = '__all__'


class PlayerClassesSerializer(serializers.ModelSerializer):
    class_abilities = serializers.PrimaryKeyRelatedField(many=True, queryset=AbilityEffects.objects.all())

    class Meta:
        model = PlayerClasses
        fields = '__all__'


class AbilitySerializer(serializers.ModelSerializer):
    ability_effects = serializers.PrimaryKeyRelatedField(many=True,
                                                         queryset=AbilityEffects.objects.all())
    ability_enhancements = serializers.PrimaryKeyRelatedField(many=True,
                                                              queryset=AbilityEnhancements.objects.all())

    class Meta:
        model = Abilities
        fields = '__all__'


class AbilityEffectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbilityEffects
        fields = '__all__'


class AbilityEnhancementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbilityEnhancements
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    characters = serializers.PrimaryKeyRelatedField(many=True, queryset=Character.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'characters')

