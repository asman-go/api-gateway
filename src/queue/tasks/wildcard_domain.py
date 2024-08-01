from celery import shared_task

from asman.queue.models import Domain, WildcardDomain


@shared_task
def format_wildcard_domain(domain: WildcardDomain) -> Domain:
    return Domain(
        domain=domain.domain.replace('*.', '')
    )
