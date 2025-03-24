def normalize_domain(domain: str) -> str:
    if domain.startswith('*.'):
        return domain[2:]

    if domain.startswith('.'):
        return domain[1:]

    return domain
