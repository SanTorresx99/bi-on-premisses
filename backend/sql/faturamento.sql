SELECT 
    -- Dados da nota
    np.id_nota_propria, 
    np.numero_nota, 
    np.status AS stts_nota, 
    np.id_empresa, 
    np.data_emissao, 
    np.id_meio_pagamento, 
    np.id_natureza_operacao, 
    np.id_situacao_documento, 
    np.id_representante, 
    np.id_condicoes_pagamento, 
    np.id_classificacao_cliente, 
    np.id_unidade_fat_cliente,

    -- Itens da nota
    inp.id_item_nota_propria, 
    inp.id_produto, 
    inp.quantidade_total AS QTD, 
    inp.valor_unitario,        
    inp.vr_produto,
    inf.vr_total, 

    -- Natureza da operação
    nop.descricao AS nat_operacao,

    -- CFOP
    cfop.codigo AS cfop, 
    cfop.descricao AS desc_cfop,

    -- Fluxo de venda
    CASE 
        WHEN mf.compoe_fluxo_venda = 1 THEN 'SIM'
        ELSE 'NÃO' 
    END AS compoe_fluxo_venda,

    -- Produto
    p.nome AS produto,
    p.altura, p.comprimento, p.largura,
    e.nome AS especie,
    se.nome AS sub_especie,
    f.nome AS fabricante,
    pcg.descricao AS pc_gerencial,
    p.data_cadastro,
    CASE WHEN p.ativo = 1 THEN 'Ativo' ELSE 'Inativo' END AS status_produto,

    -- Cliente
    cli.nome AS cliente,
    compcli.cnpj AS cpf_cnpj,
    CASE 
        WHEN CHAR_LENGTH(compcli.cnpj) = 11 THEN 'B2C'
        WHEN CHAR_LENGTH(compcli.cnpj) = 14 THEN 'B2B'
        ELSE NULL
    END AS b2b_b2c,
    rcli.nome AS regiao,
    cidcli.descricao AS cidade_cli,
    ufcli.descricao AS uf_cli,
    pcli.descricao AS pais_cli,
    gpe.nome_grupo AS grupo_pessoa,

    -- Representante
    rep.nome AS representante,

    -- Empresa

    p_emp.nome as nome_empresa,
    p_emp.nome_fantasia,
    c_emp.cnpj


FROM 
    nota_propria np 
    LEFT JOIN item_nota_propria inp ON np.id_nota_propria = inp.id_nota_fiscal_propria
    LEFT JOIN item_nota_livro_fiscal inf ON inf.id_item_nota_fiscal_propria = inp.id_item_nota_propria
    LEFT JOIN natureza_operacao nop ON nop.id_natureza_operacao = np.id_natureza_operacao
    LEFT JOIN cfop ON cfop.id_cfop = inf.id_cfop
    LEFT JOIN modelo_fiscal mf ON mf.id_modelo_fiscal = inp.id_modelo_fiscal

    -- Produto
    LEFT JOIN produto p ON p.id_produto = inp.id_produto
    LEFT JOIN especie e ON e.id_especie = p.id_especie
    LEFT JOIN sub_especie se ON se.id_sub_especie = p.id_sub_especie
    LEFT JOIN fabricante f ON f.id_fabricante = p.id_fabricante
    LEFT JOIN plano_conta_gerencial pcg ON pcg.id_plano_conta_gerencial = p.id_plano_conta_gerencial

    -- Cliente
    LEFT JOIN unidade_fat_cliente ufc ON ufc.id_unidade_fat_cliente = np.id_unidade_fat_cliente
    LEFT JOIN cliente c ON c.id_cliente = ufc.id_cliente
    LEFT JOIN pessoa cli ON cli.id_pessoa = c.id_pessoa
    LEFT JOIN complemento compcli ON compcli.id_complemento = cli.id_complemento
    LEFT JOIN regiao rcli ON rcli.id_regiao = c.id_regiao
    LEFT JOIN grupo_pessoas gpe ON gpe.id_grupo_pessoa = cli.id_grupo_pessoas
    LEFT JOIN endereco endcli ON endcli.id_endereco = ufc.id_endereco
    LEFT JOIN cidade cidcli ON cidcli.id_cidade = endcli.id_cidade
    LEFT JOIN uf ufcli ON ufcli.id_uf = cidcli.id_uf
    LEFT JOIN pais pcli ON pcli.id_pais = ufcli.id_pais

    -- Representante
    LEFT JOIN representante r ON r.id_representante = np.id_representante
    LEFT JOIN pessoa rep ON rep.id_pessoa = r.id_pessoa

    -- Empresa
    LEFT JOIN empresa emp ON emp.id_emp = np.id_empresa
    LEFT JOIN pessoa p_emp ON emp.id_pessoa = p_emp.id_pessoa
    LEFT JOIN complemento c_emp ON c_emp.id_complemento = p_emp.id_complemento

WHERE 
    np.data_emissao BETWEEN '{data_inicio}' and '{data_fim}'
    AND mf.compoe_fluxo_venda = 1
    AND e.nome LIKE '%ACABADO%';
