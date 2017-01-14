# SQuEal Program
Created a Python program that understands a SQL-like language for making queries
of data.

#Operations: 
select - followed by a comma-separated list of one or more column names in a 
table of a csv file.
from - followed by a comma-separated list of one or more csv file names.
where - followed by a comma-separated list of one or more constraints.

#Example Query: 
select a.col,b.col,c.col from tableA,tableB,tableC where a.col=b.col,a.col<c.col