from fastapi.security import OAuth2PasswordBearer

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token',
                                      scopes={"me": "Read information about the current user.",
                                              "admin": "Manage all data",
                                              "chat": "Getting access to chat with gpt model"},)
