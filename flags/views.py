import logging
import warnings

from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView

from flags.decorators import flag_check


logger = logging.getLogger(__name__)


class FlaggedViewMixin(object):
    flag_name = None
    fallback = None
    state = True

    # condition will be deprecated in a future version, use state instead
    condition = None

    @classonlymethod
    def as_view(cls, **initkwargs):
        flag_name = initkwargs.get('flag_name')
        state = initkwargs.get('state', True)
        fallback = initkwargs.get('fallback')
        condition = initkwargs.get('condition')

        if flag_name is None:
            raise ImproperlyConfigured(
                "FlaggedViewMixin requires a 'flag_name' argument."
            )

        if condition is not None:
            warnings.warn(
                'condition attribute of FlaggedViewMixin is deprecated and '
                'will be removed in a future version of Django-Flags. '
                'Please use the state attribute instead.',
                FutureWarning,
            )
            state = condition

        view = super(FlaggedViewMixin, cls).as_view(**initkwargs)

        decorator = flag_check(
            flag_name,
            state,
            fallback=fallback,
        )

        return decorator(view)


class FlaggedTemplateView(FlaggedViewMixin, TemplateView):
    pass
