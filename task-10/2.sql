select Country.Name, LiteracyRate.Rate from Country, LiteracyRate
where Country.Code == LiteracyRate.CountryCode
group by LiteracyRate.CountryCode
having max(LiteracyRate.Year) = LiteracyRate.Year
order by LiteracyRate.Rate desc
limit 1;
