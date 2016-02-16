# coding=utf-8
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from webapp.apps.accounts.models import UserProfile


class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    username = serializers.ReadOnlyField(source='user.username')
    province_id = serializers.ReadOnlyField(source='region.city.province_id')
    city_id = serializers.ReadOnlyField(source='region.city_id')
    district_id = serializers.ReadOnlyField(source='region.id')

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'avatar', 'mobile_phone','real_name', 'sex', 'birthday',
                  'interest','address', 'nickname',
                  'district_id',
                  'province_id',
                  'city_id',
                  )
        read_only_fields = ('mobile_phone', 'real_name', 'avatar',
                            'district_id',
                            'province_id',
                            'city_id',
                            )


