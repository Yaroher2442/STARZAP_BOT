from enum import Enum

token 					=	'1103934830:AAH3_r5zh9vxyMPLLdkro0V5-t4FQpgmoJo'		#	токен подключения к телеграмму

db_database_dump_file		=   'Databases\\database_dump_file.db'
db_user_dataset				=   'Databases\\user_dataset_file.db'
db_users_state_file			=	'Databases\\users_state_database.vdb'                 


class States(Enum):																#	состояния для работы ( не разобравшись не менять! )
    
    S_START 			     =	'1'
    S_START_EARNING 	     =	'2'
    S_CHOISE_METHOD 	     =	'3'
    S_EASY_SEARCH 			 =	'4'
    S_VIN_SEARCH             =  '5'
    S_OPTION                 =  '6'


