import os


def ensure_env_var(var_name: str) -> str:
    value = os.getenv(var_name)
    if value:
        return value

    import getpass

    print(f"{var_name} was not found in the environment.")
    value = getpass.getpass(f"Enter {var_name}: ")
    if value:
        os.environ[var_name] = value
    return value


if __name__ == "__main__":
    ensure_env_var("GOOGLE_API_KEY")
