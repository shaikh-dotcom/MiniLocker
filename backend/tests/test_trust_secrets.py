from minilocker.trust import real_secrets


def test_the_python_base_image_gpg_key_is_not_a_real_secret():
    env = {"GPG_KEY": "7169605F62C751356D054A26A821E680E5FA6305", "LLM_API_KEY": "sk-live-abcdef123456"}
    assert real_secrets(env) == {"LLM_API_KEY": "sk-live-abcdef123456"}


def test_other_secret_looking_names_are_still_found():
    assert "MY_SERVICE_TOKEN" in real_secrets({"MY_SERVICE_TOKEN": "abcdef0123456789"})
