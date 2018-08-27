from django.test import TestCase

from flags.conditions import CONDITIONS, register
from flags.forms import FlagStateForm


class FormTestCase(TestCase):

    def test_valid_data(self):
        form = FlagStateForm({
            'name': 'FLAG_ENABLED',
            'condition': 'boolean',
            'value': 'True'
        })
        self.assertTrue(form.is_valid())
        state = form.save()
        self.assertEqual(state.name, 'FLAG_ENABLED')
        self.assertEqual(state.condition, 'boolean')
        self.assertEqual(state.value, 'True')

    def test_blank_data(self):
        form = FlagStateForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'condition': ['This field is required.'],
            'value': ['This field is required.'],
        })

    def test_condition_choices_are_bound_late(self):
        @register('fake_condition')
        def fake_condition():
            return True

        def cleanup_condition(condition_name):
            del CONDITIONS[condition_name]

        self.addCleanup(cleanup_condition, 'fake_condition')

        form = FlagStateForm()
        self.assertIn(
            ('fake_condition', 'fake_condition'),
            form.fields['condition'].choices
        )
