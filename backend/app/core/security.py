from fastapi.security import OAuth2PasswordBearer

# ESQUEMA DE SEGURIDAD PARA EXTRAER TOKEN DE ACCESO DEL HEADER
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
