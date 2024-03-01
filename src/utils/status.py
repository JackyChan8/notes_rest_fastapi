from fastapi import status

update_status = {
    status.HTTP_204_NO_CONTENT: {
        'description': 'Changed successfully',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'null'
                }
            }
        }
    },
}

delete_status = {
    status.HTTP_204_NO_CONTENT: {
        'description': 'Delete successfully',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'null'
                }
            }
        }
    }
}

auth_status = {
    status.HTTP_401_UNAUTHORIZED: {
        'description': 'Could not validate credentials',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'detail': 'Could not validate credentials'
                    }
                }
            }
        }
    },
    status.HTTP_403_FORBIDDEN: {
        'description': 'Not authenticated',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'detail': 'string'
                    }
                }
            }
        }
    },
}
