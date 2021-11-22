alter table venda add constraint venda_produto_fk
foreign key (idProduto)
references produto (idProduto);