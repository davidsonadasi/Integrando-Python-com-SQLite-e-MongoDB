import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey, BINARY, DECIMAL
from sqlalchemy import create_engine, inspect, select, func

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "conta_cliente"
    #atributos
    id = Column(Integer, primary_key=True)
    nome = Column(String(30))
    cpf = Column(Integer)
    endereco = Column(String(30))
    
    conta = relationship("Conta", back_populates="cliente", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f" Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco}, conta={self.conta})"

class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(30))
    agencia = Column(String(30))
    num = Column(Integer)
    saldo = Column(DECIMAL, nullable=False)
    id_cliente = Column(Integer, ForeignKey("conta_cliente.id"))
    
    cliente = relationship("Cliente", back_populates="conta")
    
    def __repr__(self):
        return f"Conta (id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"
    
print(Cliente.__tablename__)
print(Conta.__table__)

# Conexao com db
engine = create_engine("sqlite://")

# Criando as classes como tabelas no db.
Base.metadata.create_all(engine)

# Investiga o db
inspetor_engine = inspect(engine)
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:    
    davidson = Cliente(
        nome="davidson",
        cpf=12345678900,
        endereco="rua um",
        conta = [Conta(tipo = 'poupanca',
                       agencia = 2020,
                       num = 2,
                       saldo = 100)
                 ]
    )
    
    Mary = Cliente(
        nome='Mary',
        cpf=98765432100,
        endereco="rua dois",
        conta = [Conta(tipo = 'Corrente',
                       agencia = 1010,
                       num = 1,
                       saldo = 100)
                 ]
    )
    
    session.add_all([davidson, Mary])
    session.commit()


stmt = select(Cliente).where(Cliente.nome.in_(['davidson','Mary']))
for client in session.scalars(stmt):
    print(client)
  
stmt_join = select(Cliente.nome,
                   Cliente.cpf, 
                   Cliente.endereco,
                   Cliente.conta,
                   Conta.id,
                   Conta.tipo, 
                   Conta.agencia,
                   Conta.num,
                   Conta.saldo).join_from(Conta, Cliente)

for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir de connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
print("\nTotal de instancias em Cliente")
for result in session.scalars(stmt_count):
    print(result)
    
#session.close()"""