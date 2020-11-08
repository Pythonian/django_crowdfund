from django.apps import AppConfig


class CrowdfundConfig(AppConfig):
    name = 'crowdfund'

    def ready(self):
    	import crowdfund.signals

