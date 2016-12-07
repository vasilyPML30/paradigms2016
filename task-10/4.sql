select Country.Name, count(case City.Population when City.Population >= 1000000 then 1 else NULL end)
from Country, City
where City.CountryCode = Country.Code
group by Country.Name
order by count(City.Id) desc, Country.Name;
