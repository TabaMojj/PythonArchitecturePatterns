from datetime import date
from typing import Optional

from domain import model
from domain.model import OrderLine
from adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(orderid: str, sku: str, qty: int, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    line = model.OrderLine(orderid, sku, qty)
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], repo: AbstractRepository, session):
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()