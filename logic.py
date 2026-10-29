RESULT_COUNTS = (3, 5, 10, 20)
SUPPORTED_TYPES = ('jpg', 'jpeg', 'png', 'webp')

def selected_count(requested, total):
    if requested not in RESULT_COUNTS:
        raise ValueError('Unsupported result count')
    return min(requested, max(0, total))
