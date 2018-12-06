from lyrebird_tracking.server.__init__ import filter_error_msg
import operator

result_dic = {
    'name': 'a',
    'asserts': [{
        'field': 'a',
        'flag': False,
        'hint': "x"
    }, {
        'field': 'b',
        'flag': False,
        'hint': 'y'
    }, {
        'field': 'c',
        'flag': True,
        'hint': "z"
    }],
    'content': {
        'a': 1
    },
}

excepted_error = {
    'name': 'a',
    'content': {
        'a': 1
    },
    'error_msg': "name: a\nerror message:\nfield: a\nerror detail: x\nfield: b\n"
                 "error detail: y\n"
}


def test_filter_error():
    error_message = dict((k, result_dic[k]) for k in ('name', 'content') if k in result_dic)
    error_message['error_msg'] = filter_error_msg(result_dic)
    assert operator.eq(excepted_error, error_message) is True
