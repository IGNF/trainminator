import os
import inspect
from qgis.core import QgsMessageLog, Qgis
from .. import NAME
# DEBUG_ENV_VAR = 'QGIS_DEBUG_ENV'

DEBUG_MODE: bool = True


def get_logger(tag=NAME):
    """
    Creates a logger function that logs messages to the QGIS Message Log.

    Parameters
    ----------
    tag : str, optional
        The tag associated with the messages. This is usually the plugin name or the main script name.

    Returns
    -------
    function
        A function that logs messages to the QGIS Message Log. The function takes two parameters:
        message (str) - The message to log.
        level (Qgis.MessageLevel) - The severity level of the message.

    Examples
    --------
    >>> logger = get_logger('MyPlugin')
    >>> logger('This is an info message', Qgis.Info)
    >>> logger('This is a warning message', Qgis.Warning)
    """

    def logger(message, level=Qgis.Info):
        """
        Logs a message to the QGIS Message Log with the specified severity level.

        Parameters
        ----------
        message : str
            The message to log.
        level : Qgis.MessageLevel, optional
            The severity level of the message (default is Qgis.Info).

        Returns
        -------
        None
        """
        # if os.environ.get('TNT_LOGGING') != '1':
        #    return
        # Get the current frame to extract file name and line number
        if DEBUG_MODE:
            frame = inspect.currentframe()
            # Go back two levels to get info about the caller of the logger function
            frame_info = inspect.getouterframes(frame)[0]
            file_name = frame_info.filename
            line_number = frame_info.lineno
            # Format the message with file name and line number
            formatted_message = f"{file_name}:{line_number} - {message}"
            # Log the message to the QGIS Message Log
            QgsMessageLog.logMessage(formatted_message, tag, level)

    return logger
