def read_api_key():
    with open('../api.txt', 'r') as f:
        api_key = f.read().strip()
    if not api_key:
        raise Exception('API key not found or empty')
    return api_key

API_KEY = read_api_key()
