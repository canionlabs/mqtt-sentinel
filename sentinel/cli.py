from __future__ import print_function, unicode_literals
import click

from PyInquirer import style_from_dict, Token, prompt

from sentinel import Sentinel
from sentinel.rules import Rule
from sentinel.output import OutMQTT


@click.group()
def ordinary():
    pass


@ordinary.command()
def run():
    """Run sentinel"""


@click.group()
def interactive():
    pass


@interactive.command('irun', short_help='Interactive setup and run sentinel')
def start_irun():
    custom_style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    def call_single_question(question_type, msg, choices=None, default=None):
        question = [
            {
                'type': question_type,
                'name': 'question',
                'message': msg,
            }
        ]
        if choices:
            question[0]['choices'] = choices
        if default is not None:
            question[0]['default'] = default

        answer = prompt(question, style=custom_style)
        return answer['question']

    sentinel = Sentinel()

    # Q-Choose a database for the rules
    db_choices = ['SQLite3 [Default]', ]
    db_answer = call_single_question(
        question_type='list',
        msg='Choose a database for the rules',
        choices=db_choices
    )
    if db_answer == 'SQLite3 [Default]':
        sentinel.set_db('sqlite://sentinel.db')

    # Q-Choose an output service
    output_choices = ['MQTT', ]
    output_answer = call_single_question(
        question_type='list',
        msg='Choose an output service',
        choices=output_choices
    )
    if output_answer == 'MQTT':
        sentinel.set_output(OutMQTT())

    # Q-Do you want add rules?
    add_rule_answer = call_single_question(
        question_type='confirm',
        msg='Do you want to add rules?',
        default=True
    )

    quit_signal = not add_rule_answer
    while not quit_signal:
        # Get topic and ask about the operation type
        rule_topic_question = [
            {
                'type': 'input',
                'name': 'topic',
                'message': 'Topic',
            },
            {
                'type': 'list',
                'name': 'operation',
                'message': 'Choose a operation:',
                'choices': [
                    'Custom parameters',
                    'Data relay',
                ]
            },
        ]
        rule_topic_answer = prompt(rule_topic_question, style=custom_style)
        if rule_topic_answer['operation'] == 'Data relay':
            rule = Rule(rule_topic_answer['topic'])
            sentinel.add_rule(rule)
        else:
            # Q-If the received value is:
            rule_operator_choices = [
                '==', '!=', '>=',
                '<=', '<', '>',
            ]
            rule_operator_answer = call_single_question(
                question_type='list',
                msg='If the received value is:',
                choices=rule_operator_choices
            )

            # Q-Value {rule_operator_answer}:'
            rule_equated_msg = (
                f'Value {str(rule_operator_answer)}')
            rule_equated_answer = call_single_question(
                question_type='input',
                msg=rule_equated_msg
            )

            rule = Rule(
                topic=rule_topic_answer['topic'],
                operator=rule_operator_answer,
                equated=rule_equated_answer
            )
            sentinel.add_rule(rule)

        # Q-Do you want to add more rules?'
        more_rule_answer = call_single_question(
            question_type='confirm',
            msg='Do you want to add more rules?',
            default=False
        )
        quit_signal = not more_rule_answer

    sentinel.start()


cli = click.CommandCollection(sources=[ordinary, interactive])

if __name__ == '__main__':
    cli()
