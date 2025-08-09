"""
API Schema customization for drf-spectacular

This module provides hooks for customizing the OpenAPI schema generation.
"""

def preprocessing_filter_spec(endpoints):
    """
    Filter and organize API endpoints for better documentation structure.
    Hides internal/admin endpoints for cleaner public documentation.
    """
    filtered_endpoints = []
    
    # Filter out admin and debug endpoints
    excluded_patterns = [
        '/api/auth/users/',  # Admin only
        '/admin/',
        '/__debug__/',
        '/static/',
        '/media/',
    ]
    
    for path, path_regex, method, callback in endpoints:
        # Skip excluded endpoints
        if any(pattern in path for pattern in excluded_patterns):
            continue
            
        # Keep all other endpoints
        filtered_endpoints.append((path, path_regex, method, callback))
    
    return filtered_endpoints


def postprocessing_hook(result, generator, request, public):
    """
    Postprocessing hook to customize the generated OpenAPI schema.
    
    Args:
        result: The generated OpenAPI schema dictionary
        generator: The schema generator instance
        request: The current request object
        public: Boolean indicating if this is for public consumption
    
    Returns:
        Modified OpenAPI schema dictionary
    """
    # Add custom info to the schema
    result['info']['contact'] = {
        'name': 'ALX Project Nexus Team',
        'email': 'support@alx-nexus.com',
        'url': 'https://github.com/devshad-01/alx-project-nexus'
    }
    
    result['info']['license'] = {
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT'
    }
    
    # Add server information
    result['servers'] = [
        {
            'url': 'http://localhost:8000/api',
            'description': 'Development server'
        },
        {
            'url': 'https://api.alx-nexus.com/api',
            'description': 'Production server'
        }
    ]
    
    # Add common response schemas
    if 'components' not in result:
        result['components'] = {}
    if 'schemas' not in result['components']:
        result['components']['schemas'] = {}
    
    # Add standard error response schemas
    result['components']['schemas']['ErrorResponse'] = {
        'type': 'object',
        'properties': {
            'error': {
                'type': 'string',
                'description': 'Error message'
            },
            'details': {
                'type': 'object',
                'description': 'Additional error details',
                'additionalProperties': True
            }
        },
        'required': ['error']
    }
    
    result['components']['schemas']['ValidationError'] = {
        'type': 'object',
        'properties': {
            'field_name': {
                'type': 'array',
                'items': {
                    'type': 'string'
                },
                'description': 'List of validation errors for this field'
            }
        },
        'additionalProperties': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
        'description': 'Field validation errors'
    }
    
    result['components']['schemas']['PaginatedResponse'] = {
        'type': 'object',
        'properties': {
            'count': {
                'type': 'integer',
                'description': 'Total number of items'
            },
            'next': {
                'type': 'string',
                'format': 'uri',
                'nullable': True,
                'description': 'URL to next page of results'
            },
            'previous': {
                'type': 'string',
                'format': 'uri',
                'nullable': True,
                'description': 'URL to previous page of results'
            },
            'results': {
                'type': 'array',
                'items': {},
                'description': 'Array of result items'
            }
        },
        'required': ['count', 'results']
    }
    
    # Add example responses to common endpoints
    if 'paths' in result:
        for path, operations in result['paths'].items():
            for method, operation in operations.items():
                # Add common error responses
                if 'responses' in operation:
                    # Add 400 validation error response to POST/PUT/PATCH operations
                    if method.upper() in ['POST', 'PUT', 'PATCH']:
                        operation['responses']['400'] = {
                            'description': 'Validation error',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        '$ref': '#/components/schemas/ValidationError'
                                    }
                                }
                            }
                        }
                    
                    # Add 401 unauthorized response to protected endpoints
                    if 'security' in operation:
                        operation['responses']['401'] = {
                            'description': 'Authentication required',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        '$ref': '#/components/schemas/ErrorResponse'
                                    },
                                    'example': {
                                        'error': 'Authentication credentials were not provided.'
                                    }
                                }
                            }
                        }
                    
                    # Add 500 server error response
                    operation['responses']['500'] = {
                        'description': 'Internal server error',
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref': '#/components/schemas/ErrorResponse'
                                }
                            }
                        }
                    }
    
    return result


def custom_schema_view_name(view):
    """
    Custom function to generate operation names for the schema.
    
    Args:
        view: The view class
    
    Returns:
        String operation name
    """
    # Extract app name and view name for better operation IDs
    if hasattr(view, '__module__'):
        module_parts = view.__module__.split('.')
        if len(module_parts) >= 2:
            app_name = module_parts[0]
            view_name = view.__class__.__name__
            return f"{app_name}_{view_name}"
    
    return view.__class__.__name__
