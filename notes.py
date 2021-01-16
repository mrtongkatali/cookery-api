## new version of select makes this
future_select(
	user_table.c.username, address_table.c.email_address
).join(address_table)

# inserting batch data
connection.execute(
	user_table.insert(),
	[
		{ "user_id": 1, "username": "Test" },
		{ "user_id": 1, "username": "Test" }
	]
)

# two table objects can be joined
join_obj = user_table.join(
	address_table, user_table.c.id == address_table.c.user_id
)

# the new version of select
select_stmt = future_select(
	user_table.c.username, address_table.c.email_address
).join(address_table)

# in order to refer to the same table multiple times in the from clause, the .alias() construct will create an alias of a table.
address_alias_1 = address_table.alias()
address_alias_2 = address_table.alias()

select_stmt = (
	select(
		[
			user_table.c.username,
			address_alias_1.c.email_address,
            address_alias_2.c.email_address,
        ]
    )
    .select_from(user_table.join(address_alias_1).join(address_alias_2))
    .where(address_alias_1.c.email_address == "spongebob")
    .where(address_alias_2.c.email_address == "spongo2")
)

# subquery is used much like a table alias, except we start with a select statement. We call the .alias(), or .subquery() method of select
stmt = select([select_subq.c.username]).where(
	select_subq.c.username == "test"
)
# To review subquery => https://youtu.be/sO7FFPNvX2s?t=6470

# COMMON TABLE EXPRESSION
adress_cte = address_select.cte()
username_plus_count = (
	select([user_table.c.username, address_cte.c.count])
	.select_from(user_table.join(address_cte))
	.order_by(user_table.c.username)
)

# Correlated sub-queries => a scalar-subquery returns only one row and a column
address_corr = (
	select([func.count(address_table.c.id)])
	.where(user_table.c.id == address_table.c.user_id)
	.as_scalar()
)

## Object Relational Mapping (ORM) => process of associating object oriented classes with datatabase tables.
# https://youtu.be/sO7FFPNvX2s?t=7557

# RELATIONSHIPS - Part 1
Base = declarative_base()
class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	username = Column(String)
	fullname = Column(String)

	addresses = relationship("Address", back_populates="user")

	def __repr__(self):
		return "<User(%r, %r)>" % (self.username, self.fullname)

# querying with multiple tables

session.query(User, Address).filter(User.id == Address.user_id)
session.query(User, Address).join(Address).all()

session.query(User.username).join(User.addressses).filter(
	Address.email_address == "123@123.com"
)

# using aliases with joins
from sqlalchemy.orm import aliased

a1, a2 = aliased(Address), aliased(Address)
session.query(User).join(a1).join(a2).filter(
	a1.email_address == "123@123.com"
).filter(
	a2.email_address == "squidward@hotmail.com"
).all()

# eager loading => solving n+1 problem
from sqlalchemy.orm import selectinload, joinedload

for user in session.query(User).options(selectinload(User.addresses)):
	print(user, user.addresses)

# using joinedload - eager loading doesn't change the result of the Query. Only how related collections are loaded.
# An explicit join() can be mixed with the joinedload() and they are kept separate
for address in (
	session.query(Address)
	.join(Address.user)
	.filter(User.username == "squidward")
	.options(joinedload(Address.user))
)

# using contains_eager
# To optimize the common case of "join to many-to-one and also load it on the object", the contain_eager() options is used
# https://stackoverflow.com/questions/26761894/join-on-a-condition-to-eagerly-load-in-sqlalchemy-orm
# https://dev.to/chidioguejiofor/eager-loading-vs-lazy-loading-in-sqlalchemy-5209
from sqlalchemy.orm import contains_eager
for address in (
	session.query(Address)
	.join(Address.user)
	.filter(User.username == "squidward")
	.options(contains_eager(Address.user))
)
