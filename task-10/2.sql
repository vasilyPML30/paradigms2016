select Country.Name from Country, LiteracyRate
group by LiteracyRate.CountryCode
having max(LiteracyRate.Year) = LiteracyRate.Year
order by LiteracyRate.Rate desc
limit 1;
