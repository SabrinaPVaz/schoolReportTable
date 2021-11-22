alter table venda add constraint venda_cliente_fk
foreign key (idCliente)
references cliente(idCliente);