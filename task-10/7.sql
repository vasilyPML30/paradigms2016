select Country.Name from Country, City
where City.CountryCode = Country.Code
group by Country.Name
having sum(City.Population) * 2 < Country.Population
order by Country.Name;