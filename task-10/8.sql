select Country.Name, Country.Population, Country.SurfaceArea from Country, Capital, City as Cap, City as Ct
where Capital.CountryCode = Country.Code
and Cap.Id = Capital.CityId
and Ct.CountryCode = Country.Code
group by Country.Name
having max(Ct.Population) = Cap.Population
order by Country.Population / Country.SurfaceArea desc, Country.Name