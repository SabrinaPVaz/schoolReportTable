create table venda(
idVenda int not null auto_increment,
dtVenda date not null,
idCliente int not null,
idProduto int not null,
primary key (idVenda)
);