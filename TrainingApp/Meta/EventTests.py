
class TestEvent:
    def __init__(self, source, event_type='Undefined', comment=''):
        self.source = source
        self.event_type = event_type
        self.comment = comment

    def __str__(self):
        return self.event_type + ':' + self.comment + '\nSource:' + self.source


class TestEventsCollector:
    main = None

    def __init__(self):
        self.feedbacks = []
        self.warnings = []
        self.errors = []
        self.print_while_run = True
        TestEventsCollector.main = self

    def collect(self, event):
        if self.print_while_run:
            print(event)
        if event.event_type == 'Feedback':
            self.feedbacks.append(event)
        if event.event_type == 'Warning':
            self.warnings.append(event)
        if event.event_type == 'Error':
            self.errors.append(event)


class TestEventsEmitter:
    def __init__(self, source_name, default_type='', default_comment=''):
        self.source_name = source_name
        self.default_type = default_type
        self.default_comment = default_comment

    def emit_feedback(self, comment=''):
        TestEventsCollector.main.collect(TestEvent(self.source_name, 'Feedback', comment))

    def emit_warning(self, comment=''):
        TestEventsCollector.main.collect(TestEvent(self.source_name, 'Warning', comment))

    def emit_error(self, comment=''):
        TestEventsCollector.main.collect(TestEvent(self.source_name, 'Error', comment))

    def default_emit(self):
        TestEventsCollector.main.collect(TestEvent(self.source_name, self.default_type, self.default_comment))
