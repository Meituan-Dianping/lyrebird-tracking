from lyrebird_tracking.server.search_handler import SearchHandler

data_list = [
    {
        "a": 3,
        "b": [
            {
                "x": "s",
                "y": [{
                    "n": "test",
                    "m": "haha"
                }, {
                    "n": "notest",
                    "m": "heihei"
                }]
            },
            {
                "x": "t",
                "y": "ooo"
            }, {
                "x": "st",
                "m": 123
            }
        ]
    }, {
        "a": 3,
        "b": [{
            "x": "st",
            "y": 456
        }, {
            "x": "st",
            "y": 789
        }, {
            "x": "s",
            "y": 123
        }]
    }
]

raw_data = {
    "haha": [
        {
            'a': 'p1', 
            'b': 'pp',
            'evs': 
            [
                {
                    'b': 'p2',
                    'x': {
                    'y': {
                        'z': [
                            {
                                'c': 'p3',
                                'core': 'gq'
                            },
                            {
                                'c': 'p2',
                                'core': 'gq1'
                            }
                        ]
                        }
                    }
            },
            {
                'b': 'p2',
                'x': {
                    'y': {
                        'z': [
                            {
                                'c': 'p33',
                                'core': 'gq3'
                            }
                        ]
                    }
                }
            }
        ]
        },
        {'a': 'p1', 'b': 'p2','evsmock': []},
        [1, 'a'],
        1,
        'b'
    ],
    "heihei": [{'a': 'p1', 'evs': []}],
    "lala": 123
}


def test_transfer_query():
    jsonpath_str = "$[?ca='travel'].evs[?vb='yf']"
    search_list = SearchHandler().transfer_query(jsonpath_str)
    assert search_list == ["[?ca='travel']", "evs", "[?vb='yf']"]

    jsonpath_str = "$haha[?a='p1'].evs[?b='p2'].x.y.z[?c='p3']"
    search_list = SearchHandler().transfer_query(jsonpath_str)
    assert search_list == ["haha", "[?a='p1']", "evs", "[?b='p2']", "x", "y", "z", "[?c='p3']"]


def test_query1():
    jsonpath_str = "$haha[?a='p1'].evs[?b='p2'].x.y.z[?c='p3']"
    node = SearchHandler(raw_data)
    result = node.find(jsonpath_str).data
    assert len(result) == 1
    assert result[0]['core'] == 'gq'


def test_query2():
    jsonpath_str = "haha[?a='p1'].evs[?b='p2'].x.y.z[?c='p3']"
    node = SearchHandler(raw_data)
    result = node.find(jsonpath_str).data
    assert len(result) == 1
    assert result[0]['core'] == 'gq'


def test_query3():
    jsonpath_str = "$haha[?a='p1'].$evs[?b='p2'].x.y.z[?c='p3']"
    node = SearchHandler(raw_data)
    result = node.find(jsonpath_str).data
    assert len(result) == 0


def test_query4():
    jsonpath_str = "$[?a=3].b[?x='s']"
    node = SearchHandler(data_list)
    result = node.find(jsonpath_str).data
    assert len(result) == 2
    assert result[1]['y'] == 123
    assert result[0]['y'][0]['n'] == 'test'


def test_query5():
    jsonpath_str = "$[*].b[?x='st']"
    node = SearchHandler(data_list)
    result = node.find(jsonpath_str).data
    assert len(result) == 3
    assert result[0]['m'] == 123
    assert result[1]['y'] == 456
    assert result[2]['y'] == 789


def test_query6():
    jsonpath_str = "$[2].b[?x='st']"
    node = SearchHandler(data_list)
    result = node.find(jsonpath_str).data
    assert len(result) == 0


def test_query7():
    jsonpath_str = "$[1].b[?x='st']"
    node = SearchHandler(data_list)
    result = node.find(jsonpath_str).data
    assert len(result) == 2
    assert result[0]['y'] == 456
    assert result[1]['y'] == 789


def test_query8():
    jsonpath_str = "$haha[?a='p1'].evs[*].x.y.z[?c='p3']"
    node = SearchHandler(raw_data)
    result = node.find(jsonpath_str).data
    assert len(result) == 1
    assert result[0]['core'] == 'gq'


def test_query9():
    jsonpath_str = "$haha[?a='p1'].evs[*].x.y.z"
    node = SearchHandler(raw_data)
    result = node.find(jsonpath_str).data
    assert len(result) == 2
    assert result[1][0]['c'] == 'p33'


def test_query10():
    jsonpath_str = "$haha[?a='p1'&b='pp'].evs[*].x.y.z"
    node = SearchHandler(raw_data)
    result = node.find(jsonpath_str).data
    assert len(result) == 2
    assert result[1][0]['c'] == 'p33'