
import os
from .caller import Caller
from .remotejit import RemoteJIT
from .thrift.utils import resolve_includes
from pymapd.cursor import make_row_results_set
from pymapd._parsers import (_extract_description, _bind_parameters)

def _make_row_results_set(data):
    # copied from pymapd.cursor.py
    if data.row_set.is_columnar:
        if data.row_set.columns:
            nrows = len(data.row_set.columns[0].nulls)
            ncols = len(data.row_set.row_desc)
            columns = [_extract_col_vals(desc, col)
                       for desc, col in zip(data.row_set.row_desc,
                                            data.row_set.columns)]
            for i in range(nrows):
                yield tuple(columns[j][i] for j in range(ncols))
    else:
        for row in data.row_set.rows:
            yield tuple(_extract_row_val(desc, val)
                        for desc, val in zip(data.row_set.row_desc, row.cols))

class CallerMapD(Caller):
    """
    """

    def call(self, name, *args):
        return self.client(MapD={name: args})['MapD'][name]
        
    
    def get_MapD_version(self):
        return self.call('get_version')

    _session_id = None
    @property
    def session_id(self):
        if self._session_id is None:
            user = self.remotejit.user
            pw = self.remotejit.password
            dbname = self.remotejit.dbname
            self._session_id = self.call('connect', user, pw, dbname)
        return self._session_id

    def sql_execute(self, query):
        columnar = True
        result = self.call('sql_execute', self.session_id, query, columnar, "", -1, -1)

        descr = _extract_description(result.row_set.row_desc)
        return descr, make_row_results_set(result)

    def register(self):
        signatures = self._signatures
        ir = self.get_IR(signatures)
        mangled_signatures = [s.mangle() for s in signatures]
        return self.call('register_function', self.session_id, self.func.__name__, mangled_signatures, ir)


class RemoteMapD(RemoteJIT):

    """
    Usage:

      mapd = RemoteMapD(host=..., port=...)

      @mapd
      def add(a, b):
          return a + b

      add.register()

      Use pymapd, for instance, to make a SQL query `select add(c1, c2) from table`

    """

    caller_cls = CallerMapD
    multiplexed = False

    def __init__(self,
                 user='mapd',
                 password='HyperInteractive',
                 host='127.0.0.1',
                 port=6274,
                 dbname='mapd',
                 **options):
        self.user = user
        self.password = password
        self.dbname = dbname

        thrift_filename = '/home/pearu/git/Quansight/mapd-core-internal/mapd.thrift'
        self.thrift_content = resolve_includes(open(thrift_filename).read(), [os.path.dirname(thrift_filename)]).replace('completion_hints.', '')
        RemoteJIT.__init__(self, host=host, port=port, **options)