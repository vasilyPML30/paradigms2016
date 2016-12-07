select City.Name from City, Capital, Country
where Country.Name = "Malaysia"
and Capital.CountryCode = Country.Code
and City.Id = Capital.CityId;
