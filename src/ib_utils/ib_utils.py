from ib_async import IB
from contextlib import contextmanager


def _is_notebook() -> bool:
    """Check whether the code is running in an interactive notebook environment.

    Returns:
        bool: ``True`` if running in a Jupyter notebook (e.g., JupyterLab),
        ``False`` otherwise.
    """
    try:
        from IPython import get_ipython  # type: ignore

        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Notebook or JupyterLab
        elif shell == "TerminalInteractiveShell":
            return False  # IPython in a terminal
        else:
            return False  # Other environments (e.g., Google Colab, Spyder)
    except (NameError, ImportError):
        return False  # Standard Python script


def _ib_connect(host: str = "127.0.0.1", port: int = 4002, clientId: int = 1) -> IB:
    """Establish a connection to Interactive Brokers Gateway or TWS.

    Args:
        host (str, optional): Host address for the connection.
            Defaults to ``"127.0.0.1"``.
        port (int, optional): Port number to connect to.
            Use ``4002`` for paper trading (IB Gateway) or ``4001`` for live trading.
            Defaults to ``4002``.
        clientId (int, optional): Unique client identifier for the session.
            Defaults to ``1``.

    Returns:
        IB: An active IB connection instance for performing trading operations.
    """
    from ib_async import IB, util

    if _is_notebook():
        util.startLoop()
    ib = IB()
    ib.connect(host, port, clientId)
    return ib


def _ib_disconnect(ib: IB):
    """Close an active Interactive Brokers connection.

    Args:
        ib (IB): The IB instance to disconnect.
    """
    ib.disconnect()


@contextmanager
def ib_session(host: str = "127.0.0.1", port: int = 4002, clientId: int = 1):
    """Context manager for simplified Interactive Brokers sessions.

    This context manager automatically handles the connection setup and
    ensures the disconnection of the IB instance, eliminating the need for
    explicit ``try/finally`` blocks.

    Args:
        host (str, optional): Host address for the connection.
            Defaults to ``"127.0.0.1"``.
        port (int, optional): Port number to connect to.
            Use ``4002`` for paper trading (IB Gateway) or ``4001`` for live trading.
            Defaults to ``4002``.
        clientId (int, optional): Unique client identifier for the session.
            Defaults to ``1``.

    Yields:
        IB: An active IB connection instance for performing trading operations.
    """
    try:
        ib: IB = _ib_connect(host, port, clientId)
        yield ib
    finally:
        _ib_disconnect(ib)
