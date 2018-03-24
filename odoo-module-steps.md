# Odoo First Steps de um Modulo

## 1. Inicio
Criando o modulo a partir de um scaffold:

$ odoo-bin scaffold <module name> <where to put it>

Em seguida adaptar o _manifest_.py para representar as funcionalidades do seu modulo.


## 2. Definindo um modelo
*** Apenas se for necessário ***

### 2.1 Arquivo models/models.py
Ex:
```python
from odoo import models, fields, api
class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
```

### 2.2 Arquivo de dados
Dados de modulo são declarados via XML com tag ```<record>```, cada elemento ```<record>``` cria ou atualiza uma entrada do banco.

Exemplo:
```xml
<odoo>
        <record model="{model name}" id="{record identifier}">
            <field name="{a field name}">{a value}</field>
        </record>
</odoo>
```

Onde:
- ```model``` é o nome do modelo para o record
- ```id``` é um identificador externo, permite referenciar o dado sem que se saiba o identificado na base de dados.
- ```<field>``` elementos possuem um "name" que pe o nome do campo no modelo, e possuem o valor de tal campo em seu corpo.

Os 'dados' devem ser declarados no arquivo manifest para serem
carregados sempre, ou declarados em 'demo' para carregarem junto ao modo de demonstração (demo/demo.xml), e podem possuir multiplas entradas de dados.

Após as alterações é necessário a execução do comando:
```$ odoo-bin -u <module name>```
Para que as alterações sejam efetivadas na base de dados.

## 3. Ações e Menus
São representados como ```records``` na base de dados, normalmente declarado por arquivos de dados (xml). E as ações podem ser disparados por 3 maneiras:

1. Clicando no menu item
2. Clicando em botões em uma view
3. Como ações de um objeto

Devido a sua complexidade de declaração, existe um atalho ```<menuitem>``` para declarar um ```ir.ui.menu``` e conectar a ação correspondente de uma maneira fácil.

Exemplo:
```xml
<record model="ir.actions.act_window" id="action_list_ideas">
    <field name="name">Ideas</field>
    <field name="res_model">idea.idea</field>
    <field name="view_mode">tree,form</field>
</record>
<menuitem id="menu_ideas" parent="menu_root" name="Ideas"
            sequence="10" action="action_list_ideas"/>
```


**Cuidado**: A ação deve ser declarada antes do menu correspondente no arquivo XML.
Arquivos de dados são executados sequencialmente, os id's de ações devem estar presentes na base de dados antes do menu ser criado.

## 4. Views Básicas
Views definem como um ```record``` de um modelo é exibido. Cada tipo de vire representa um modo de visualização (lista de records, grafico de agregação,...). Podem ser ou requisitadas genericamente ou especificamente por id.
Para requisições genéricas, a view com tipo correto e a menor prioridade será usada (então a view de menor prioridade é a view padrão para tal tipo).

OBS: **View Inheritance** permite alterar views (adicionar ou remover conteudo).

### 4.1 Declaração genérica
Uma view é decalrada como um record do modelo `ir.ui.view`. O tipo da view é implicita pelo campo `arch` do elemento raiz:

```xml
<record model="ir.ui.view" id="view_id">
    <field name="name">view.name</field>
    <field name="model">object_name</field>
    <field name="priority" eval="16"/>
    <field name="arch" type="xml">
        <!-- view content: <form>, <tree>, <graph>, ... -->
    </field>
</record>
```

OBS: O campo `arch` deve ser declarado como `type="xml"` para ser parseado corretamente.

#### 4.1.1 Tree view
Também chamada de list view, exibe os records em formato tabular.
O elemento rais é `<tree>`. A forma mais simples da tree view lista todos os campos para exibir na tabela (cada campo como uma coluna):

```xml
<tree string="Idea list">
    <field name="name"/>
    <field name="inventor_id"/>
</tree>
```
#### 4.1.2 Form view
Forms são usados para criar e editar um único record. O elemento raiz é `<form>`.  É composto de elementos estruturais como grupos e notebooks, e elementos interativos, botões e campos:
```xml
<form string="Idea form">
    <group colspan="4">
        <group colspan="2" col="2">
            <separator string="General stuff" colspan="2"/>
            <field name="name"/>
            <field name="inventor_id"/>
        </group>

        <group colspan="2" col="2">
            <separator string="Dates" colspan="2"/>
            <field name="active"/>
            <field name="invent_date" readonly="1"/>
        </group>

        <notebook colspan="4">
            <page string="Description">
                <field name="description" nolabel="1"/>
            </page>
        </notebook>

        <field name="state"/>
    </group>
</form>
```

Forms também podem ser usados com HTML puro, para layouts mais flexíveis:
```html
<form string="Idea Form">
    <header>
        <button string="Confirm" type="object" name="action_confirm"
                states="draft" class="oe_highlight" />
        <button string="Mark as done" type="object" name="action_done"
                states="confirmed" class="oe_highlight"/>
        <button string="Reset to draft" type="object" name="action_draft"
                states="confirmed,done" />
        <field name="state" widget="statusbar"/>
    </header>
    <sheet>
        <div class="oe_title">
            <label for="name" class="oe_edit_only" string="Idea Name" />
            <h1><field name="name" /></h1>
        </div>
        <separator string="General" colspan="2" />
        <group colspan="2" col="2">
            <field name="description" placeholder="Idea description..." />
        </group>
    </sheet>
</form>
```


#### 4.1.3 Search view
Views de busca customizão o campo de busca associado com a list view (e outras views agregadas). O elemento raiz é `<search>`, composto pelos campos definindo quais itens podem ser pesquisados.

```xml
<search>
    <field name="name"/>
    <field name="inventor_id"/>
</search>
```
Se nenhuma busca existe, Odoo gera uma que permite apenas a busca pelo campo `name`.

## 5. Relações entre modelos
Um record de um modelo pode ser relacionado a um record de outro model. Por exemplo, Odem de venda é relacionado a um record Cliente que contém os dados do cliente, que é também relacionado aos records de suas ordens de compra.

### 5.1 Campos relacionais
Campos relacionais relacionam records, sejam do mesmo modelo (heirarquico) ou entre diferentes modelos.

1. Many2one(other_model, ondelete='set null')
    - Link simples com um outro objeto

2. One2many(other_model, related_field)
    - Relacionamento inverso ao `Many2one`. Um `One2many` se comporta como um container de records, ao se acessar o relacionamento, produz um conjunto de resultados, possivelmente vazios.
    - OBS: como `One2many` é um relacionamento virtual, deve existir um campo `Many2one` no modelo `other_model`, e seu nome deve ser `related_field`

3. Many2many(other_model)
    - Relacionamento bidirecional multiplo, qualquer record em um lado pode ser relacionado a vários records de outro modelo. Se comporta como um container de records, ao se acessar o relacionamento, produz um conjunto de resultados, possivelmente vazios.

## 6. Inheritance

### 6.1 Model Inheritance
Odoo provê dois mecanismos de herança para extender um modelo existente de forma modular.
O primeiro mecanismo permite que um modulo modifique o comportamento de um modelo definido em outro modulo:

- Adicionar campos a um modelo.
- Sobreescrever a definição de campos em um modelo.
- Adicionar restrições a um modelo.
- Adicionar métodos a um modelo.
- Sobreescrever métodos existentes em um modelo.

O segundo mecanismo (delegation) permite ligar cada record de um modelo a um record de um modelo pai, e provê acesso transparente para os campos do modelo pai.

[Documentação de herança do odoo](http://www.odoo.com/documentation/11.0/howtos/backend.html#inheritance)


### 6.1 View Inheritance
No lugar de modificar views existentes, Odoo provê 



