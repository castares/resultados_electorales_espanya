import polars as pl
import polars.selectors as cs

df = pl.read_csv("./data/csv/congreso_2019.csv")

df = df.rename({col: col.strip() for col in df.columns})

cleaned_cols = df.select(
    pl.col("Nombre de Comunidad").str.strip(),
    pl.col("Código de Provincia"),
    pl.col("Nombre de Provincia").str.strip(),
    pl.col("Código de Municipio"),
    pl.col("Nombre de Municipio").str.strip(),
)

df = cleaned_cols.join(
    df.select(cs.numeric()),
    on=["Código de Provincia", "Código de Municipio"],
    how="left",
)

df.write_csv("./data/cleaned_data/cleaned_congreso_2019.csv", separator=",")
