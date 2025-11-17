class Except:
    @staticmethod
    def not_allowed_403() -> str:
        """
        Return a message indicating that the user does not have permission to perform this action.

        Returns:
            str: A message indicating lack of permission.
        """
        return "You do not have enough permissions to perform this action."

    @staticmethod
    def user_not_found_404(user_id: int) -> str:
        """
        Return a message indicating that the user with the specified ID was not found.

        Args:
            user_id (int): The ID of the user.

        Returns:
            str: A message indicating the user was not found.
        """
        return f"User with ID {user_id} not found."

    @staticmethod
    def error_deleting_user(user_id: int, error: str) -> str:
        """
        Return a message indicating an error occurred while deleting the user.

        Args:
            user_id (int): The ID of the user.
            error (str): The error message.

        Returns:
            str: A message indicating the error occurred during user deletion.
        """
        return f"Error deleting user {user_id}: {error}."

    @staticmethod
    def error_retrieving_user(user_id: int, error: str) -> str:
        """
        Return a message indicating an error occurred while retrieving the user.

        Args:
            user_id (int): The ID of the user.
            error (str): The error message.

        Returns:
            str: A message indicating the error occurred during user retrieval.
        """
        return f"Error retrieving user {user_id}: {error}."

    @staticmethod
    def error_updating_user(user_id: int, error: str) -> str:
        """
        Return a message indicating an error occurred while updating the user.

        Args:
            user_id (int): The ID of the user.
            error (str): The error message.

        Returns:
            str: A message indicating the error occurred during user update.
        """
        return f"Error updating user {user_id}: {error}."

    @staticmethod
    def error_creating_user(error: str) -> str:
        """
        Return a message indicating an error occurred while creating the user.

        Args:
            error (str): The error message.

        Returns:
            str: A message indicating the error occurred during user creation.
        """
        return f"Error creating user: {error}."

    @staticmethod
    def bad_request_400(item: str) -> str:
        """
        Return a message indicating the same Item already exists

        Args:
            error (str): The error message.
            item (str): The item name

        Returns:
            str: A message indicating the error occurred during user creation.
        """
        return f"{item} already exists."
