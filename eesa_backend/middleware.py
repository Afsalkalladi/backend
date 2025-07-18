"""
Database Connection Error Handler Middleware
This middleware handles PostgreSQL cursor errors and automatically reconnects.
"""

import logging
from django.db import connection
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class DatabaseErrorHandlerMiddleware(MiddlewareMixin):
    """
    Middleware to handle database connection errors and automatically reconnect.
    """
    
    def process_exception(self, request, exception):
        """Handle database connection exceptions"""
        
        # Check if it's a PostgreSQL cursor error
        error_messages = [
            'cursor',
            'does not exist',
            'InvalidCursorName',
            'OperationalError'
        ]
        
        if any(msg in str(exception) for msg in error_messages):
            logger.warning(f"Database connection error detected: {exception}")
            
            try:
                # Close the problematic connection
                connection.close()
                logger.info("Closed database connection due to cursor error")
                
                # For admin interface, redirect to retry
                if '/admin/' in request.path or '/eesa/' in request.path:
                    return HttpResponse(
                        """
                        <html>
                        <head>
                            <title>Database Connection Issue</title>
                            <meta http-equiv="refresh" content="2">
                        </head>
                        <body>
                            <h2>Database connection issue detected.</h2>
                            <p>Reconnecting... Please wait.</p>
                            <script>
                                setTimeout(function() {
                                    window.location.reload();
                                }, 2000);
                            </script>
                        </body>
                        </html>
                        """,
                        status=503
                    )
                    
            except Exception as e:
                logger.error(f"Error handling database connection: {e}")
        
        # Let other exceptions pass through
        return None
