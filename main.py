import argparse
import sys
import classic_main
import mainQ
import main_gui


def _cli_classic():
    """Consola normal: Humano vs Humano, Humano vs Bot, Bot vs Bot."""
    from classic_main import main as cli_main
    cli_main()


def _cli_quantum():
    """Consola cuántica: incluye Quantum Bot vs Quantum Bot, etc."""
    from mainQ import main as q_main
    q_main()


def _gui_classic():
    """Ventana gráfica con Pygame (modos clásicos)."""
    from main_gui import main as gui_main
    gui_main()


def _gui_quantum():
    """Ventana gráfica con los modos cuánticos añadidos."""
    import QuantumAppExtension  # noqa: F401
    from View.App import TicTacToeApp

    app = TicTacToeApp()
    app.run()


def main():
    parser = argparse.ArgumentParser(
        description="TIC-TAC-TOE // QUANTUM GRID - Lanzador único"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Forzar modo consola (texto). Es el default si no se pasa --gui.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Abrir la ventana gráfica con Pygame.",
    )
    parser.add_argument(
        "--quantum",
        action="store_true",
        help="Activar los bots cuánticos (funciona con --cli y --gui).",
    )
    args = parser.parse_args()

    if not args.gui:
        args.cli = True

    try:
        if args.gui and args.quantum:
            _gui_quantum()
        elif args.gui:
            _gui_classic()
        elif args.quantum:
            _cli_quantum()
        else:
            _cli_classic()
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario. ¡Hasta luego!")
        sys.exit(0)

if __name__ == "__main__":
    main()