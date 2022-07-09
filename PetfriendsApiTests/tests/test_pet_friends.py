from api import PetFriends
from settings import *
import os

class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_get_all_pets_with_valid_key(self, filter=''):  # filter available values : my_pets
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_add_new_pet_with_valid_data(self, name='Барбоскин', animal_type='двортерьер',
                                         age='4', pet_photo='images/cat1.jpg'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_successful_delete_self_pet(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
            _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        pet_id = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()

    def test_successful_update_self_pet_info(self, name='Мурзик', animal_type='Котэ', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

    def test_post_add_pet_without_photo(self, name='Барбоскин', animal_type='двортерьер', age='4'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
        assert status == 200
        """проверяем что питомец без фото добавился сравнением имени из ответа API и имени добавленного питомца"""
        assert result['name'] == name


    def test_post_add_pet_foto(self, pet_photo='images/cat1.jpg'):

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        self.pf.add_new_pet_without_photo(auth_key, "Миша", "медведь", "3")
        """добавляем питомца без фото"""
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")
        pet_id = my_pets['pets'][0]['id']

        pet_photo1 = my_pets['pets'][0]['pet_photo']
        """берем фото последнего добавленного питомца, по факту фото нет"""
        status, result = self.pf.add_pet_photo(auth_key, pet_id, pet_photo)

        assert status == 200
        """"Сравниваем фото питомца до и после добавления фото"""
        assert pet_photo != pet_photo1

    def test_add_new_pet_with_invalid_data(self, name='Барбоскин', animal_type='двортерьер', age='4', pet_photo='images/doc.docx'):
        """вставляем в фото файл другого формата .doc"""
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")
        pet_id = my_pets['pets'][0]['id']
        pet_photo1 = my_pets['pets'][0]['pet_photo']

        assert status == 200
        """Проверяем, что неприемлемый файл в фото не вставился"""
        assert pet_photo1 == ''

    def test_get_api_key_for_invalid_email(self, email=invalid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403
        assert not 'key' in result

    def test_get_api_key_for_invalid_passw(self, email=valid_email, password=invalid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403
        assert not 'key' in result

    def test_get_api_key_for_swapped_passw_email(self, email=valid_password, password=valid_email):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403
        assert not 'key' in result

    def test_add_new_pet_with_name_only(self, name='Гриня', animal_type='',
                                         age=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet_without_photo(auth_key, name,  animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert result['age'] == ''

    def test_post_add_pet_with_too_big_age(self, name='Барбоскин', animal_type='двортерьер', age='10000000000000000000000000'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
        """ожидаем ошибку пользователя, но такой возраст проходит, тест заваливается"""
        assert status == 400

    def test_post_add_pet_with_number_in_name(self, name='29292929', animal_type='двортерьер',
                                           age='23'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
        """ожидаем ошибку пользователя, но такое имя проходит, тест заваливается"""
        assert status == 400

    def test_add_new_pet_with_photo_instead_name(self, name='images/cat1.jpg', animal_type='двортерьер',
                                         age='4', pet_photo='images/cat1.jpg'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)

        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        """ожидаем ошибку пользователя, но такое имя проходит, тест заваливается"""
        assert status == 400
