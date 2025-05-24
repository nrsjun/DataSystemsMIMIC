import streamlit_authenticator as stauth

passwords = ['admin', 'password1', 'password2']

hashed_passwords = [stauth.Hasher().hash(pw) for pw in passwords]

print(hashed_passwords)


#manager: $2b$12$MA4GvCaxizAW.BVH7Aff2O7BQ03TXULwSo0gnyeWJVxmAVU1lcrVu

#clinician1: $2b$12$ejwp58/wG1CwAJhKqEbbwOW60uwyrJv2USbNp8bgfre.deQWkYYBW

#clinician2: $2b$12$/ndAwPS/2pBdagziqsKRmOR2c1Wox8ikdhTQoCL5gxpJiH8WlUNBu