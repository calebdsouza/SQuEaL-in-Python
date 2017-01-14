# SQuEal Program
Created a Python program that understands a SQL-like language for making queries<br />
of data.<br />

#Operations: 
select - followed by a comma-separated list of one or more column names in a<br /> 
table of a csv file.<br />
from - followed by a comma-separated list of one or more csv file names.<br />
where - followed by a comma-separated list of one or more constraints.<br />

#Example Query: 
select a.col,b.col,c.col from tableA,tableB,tableC where a.col=b.col,a.col<c.col<br />