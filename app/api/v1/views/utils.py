"""contains helper functions to routes"""
def wrap_response(status_code, data):
    """wraps response according to api specification"""
    wrapper = "data" if 200 <= status_code < 300 else "error"
    return {
        "status":status_code,
        wrapper:data
    }
