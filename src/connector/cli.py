import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import typer

from connector.registry import get_registry

app = typer.Typer(help="qtcloud-think 连接器管理工具")


@app.command()
def list_connectors():
    """列出所有已安装的连接器"""
    registry = get_registry()
    names = registry.names()

    if not names:
        typer.echo("未找到任何连接器插件")
        return

    typer.echo(f"已安装的连接器 ({len(names)} 个)：\n")
    for name in names:
        connector_class = registry.get(name)
        if connector_class:
            typer.echo(f"  • {name}")
            if hasattr(connector_class, "description"):
                typer.echo(f"    {connector_class.description}")
    typer.echo("")


@app.command()
def info(name: str):
    """查看连接器详细信息"""
    registry = get_registry()
    connector_class = registry.get(name)

    if not connector_class:
        typer.echo(f"未找到名为 '{name}' 的连接器")
        raise typer.Exit(1)

    typer.echo(f"连接器: {name}")
    typer.echo(f"类名: {connector_class.__name__}")
    typer.echo(f"模块: {connector_class.__module__}")

    if hasattr(connector_class, "description"):
        typer.echo(f"描述: {connector_class.description}")


def main():
    app()


if __name__ == "__main__":
    main()
