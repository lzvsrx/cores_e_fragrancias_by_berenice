import streamlit as st
import os
from datetime import datetime
from utils.database import (
    add_produto, get_all_produtos, update_produto, delete_produto, get_produto_by_id,
    export_produtos_to_csv, import_produtos_from_csv, generate_stock_pdf,
    get_all_marcas, get_all_estilos, get_all_tipos
)

st.set_page_config(page_title="Gerenciar Produtos - Cores e Fragrâncias")

def add_product_form():
    st.subheader("Adicionar Novo Produto")
    
    # Get all available categories from the database
    marcas = [m.get('nome') for m in get_all_marcas()]
    estilos = [e.get('nome') for e in get_all_estilos()]
    tipos = [t.get('nome') for t in get_all_tipos()]
    
    with st.form("add_product_form", clear_on_submit=True):
        nome = st.text_input("Nome do Produto", max_chars=150)
        col1, col2 = st.columns(2)
        with col1:
            preco = st.number_input("Preço (R$)", min_value=0.00, format="%.2f")
        with col2:
            quantidade = st.number_input("Quantidade", min_value=0, step=1)
        
        # Use the lists from the database to populate the select boxes
        marca = st.selectbox("Marca", sorted(marcas))
        estilo = st.selectbox("Estilo", sorted(estilos))
        tipo = st.selectbox("Tipo de Produto", sorted(tipos))
        
        data_validade = st.date_input("Data de Validade")
        foto = st.file_uploader("Adicionar Foto do Produto", type=["jpg", "png", "jpeg"])
        submitted = st.form_submit_button("Adicionar Produto")

        if submitted:
            if not nome:
                st.error("Nome é obrigatório.")
                return
            photo_name = None
            if foto:
                photo_name = f"{int(datetime.now().timestamp())}_{foto.name}"
                with open(os.path.join("assets", photo_name), "wb") as f:
                    f.write(foto.getbuffer())
            add_produto(nome, float(preco), int(quantidade), marca, estilo, tipo, photo_name, data_validade.isoformat())
            st.success(f"Produto '{nome}' adicionado com sucesso!")
            st.experimental_rerun()

def manage_products_list():
    st.subheader("Lista de Produtos")
    produtos = get_all_produtos()
    if not produtos:
        st.info("Nenhum produto cadastrado.")
        return

    # Top action buttons: CSV export/import, PDF report
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        if st.button('Exportar CSV'):
            csv_path = os.path.join('data','produtos_export.csv')
            try:
                export_produtos_to_csv(csv_path)
                st.success('CSV exportado para ' + csv_path)
                st.download_button('Baixar CSV', data=open(csv_path,'rb').read(), file_name='produtos_export.csv')
            except Exception as e:
                st.error('Erro ao exportar CSV: ' + str(e))
    with col_b:
        uploaded_csv = st.file_uploader('Importar CSV', type=['csv'], key='import_csv')
        if uploaded_csv is not None:
            save_path = os.path.join('data','import_tmp.csv')
            with open(save_path,'wb') as f:
                f.write(uploaded_csv.getbuffer())
            try:
                import_produtos_from_csv(save_path)
                st.success('Produtos importados com sucesso.')
                st.experimental_rerun()
            except Exception as e:
                st.error('Erro ao importar CSV: ' + str(e))
    with col_c:
        if st.button('Gerar Relatório PDF'):
            pdf_path = os.path.join('data','relatorio_estoque.pdf')
            try:
                generate_stock_pdf(pdf_path)
                st.success('PDF gerado: ' + pdf_path)
                with open(pdf_path,'rb') as f:
                    st.download_button('Baixar PDF', data=f.read(), file_name='relatorio_estoque.pdf')
            except Exception as e:
                st.error('Erro ao gerar PDF: ' + str(e))

    for p in produtos:
        produto_id = p.get("id")
        # Improved card-like layout
        with st.container():
            cols = st.columns([3,1,1])
            with cols[0]:
                st.markdown(f"### {p.get('nome')}  <small style='color:gray'>ID: {produto_id}</small>", unsafe_allow_html=True)
                st.write(f"**Preço:** R$ {float(p.get('preco')):.2f}    •    **Quantidade:** {p.get('quantidade')}")
                st.write(f"**Marca:** {p.get('marca')}    •    **Estilo:** {p.get('estilo')}    •    **Tipo:** {p.get('tipo')}")
                st.write(f"**Validade:** {p.get('data_validade') or '-'}")
            with cols[1]:
                if p.get('foto') and os.path.exists(os.path.join('assets', p.get('foto'))):
                    st.image(os.path.join('assets', p.get('foto')), width=120)
                else:
                    st.info('Sem foto')
            with cols[2]:
                role = st.session_state.get('role','staff')
                # Only admins can delete products; staff can add/edit
                if st.button('Editar', key=f'mod_{produto_id}'):
                    st.session_state['edit_product_id'] = produto_id
                    st.session_state['edit_mode'] = True
                    st.experimental_rerun()
                if role == 'admin':
                    if st.button('Remover', key=f'rem_{produto_id}'):
                        delete_produto(produto_id)
                        st.warning(f"Produto '{p.get('nome')}' removido.")
                        st.experimental_rerun()
                else:
                    st.text('Remover (admin)')

    if st.session_state.get('edit_mode'):
        show_edit_form()

def show_edit_form():
    produto_id = st.session_state.get('edit_product_id')
    produto = get_produto_by_id(produto_id)
    if not produto:
        st.error("Produto não encontrado.")
        st.session_state["edit_mode"] = False
        return

    # Get all available categories from the database
    marcas = [m.get('nome') for m in get_all_marcas()]
    estilos = [e.get('nome') for e in get_all_estilos()]
    tipos = [t.get('nome') for t in get_all_tipos()]
    
    st.subheader(f"Editar Produto: {produto.get('nome')}")
    with st.form("edit_product_form"):
        nome = st.text_input("Nome", value=produto.get("nome"))
        col1, col2 = st.columns(2)
        with col1:
            preco = st.number_input("Preço (R$)", value=float(produto.get("preco")), format="%.2f")
        with col2:
            quantidade = st.number_input("Quantidade", value=int(produto.get("quantidade")), step=1)
        
        # Use the lists from the database to populate the select boxes
        marca = st.selectbox("Marca", sorted(marcas), index=sorted(marcas).index(produto.get("marca")) if produto.get("marca") in sorted(marcas) else 0)
        estilo = st.selectbox("Estilo", sorted(estilos), index=sorted(estilos).index(produto.get("estilo")) if produto.get("estilo") in sorted(estilos) else 0)
        tipo = st.selectbox("Tipo", sorted(tipos), index=sorted(tipos).index(produto.get("tipo")) if produto.get("tipo") in sorted(tipos) else 0)
        
        data_validade = st.date_input("Data de Validade", value=datetime.fromisoformat(produto.get("data_validade")).date() if produto.get("data_validade") else None)
        uploaded = st.file_uploader("Alterar Foto", type=["jpg","png","jpeg"])
        save = st.form_submit_button("Salvar Alterações")

        if save:
            photo_name = produto.get("foto")
            if uploaded:
                photo_name = f"{int(datetime.now().timestamp())}_{uploaded.name}"
                with open(os.path.join("assets", photo_name), "wb") as f:
                    f.write(uploaded.getbuffer())

            update_produto(produto_id, nome, float(preco), int(quantidade), marca, estilo, tipo, photo_name, data_validade.isoformat())
            st.success("Produto atualizado com sucesso!")
            st.session_state["edit_mode"] = False
            st.experimental_rerun()

# Main page logic
if not st.session_state.get("logged_in"):
    st.error("Acesso negado. Faça login na área administrativa para gerenciar produtos.")
    st.info("Vá para a página 'Área Administrativa' para entrar ou criar um admin.")
else:
    st.sidebar.markdown(f"**Olá, {st.session_state.get('username')} ({st.session_state.get('role','staff')})**")
    action = st.sidebar.selectbox("Ação", ["Adicionar Produto", "Visualizar / Modificar / Remover Produtos"])
    if action == "Adicionar Produto":
        add_product_form()
    else:
        manage_products_list()
