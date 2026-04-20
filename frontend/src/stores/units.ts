type LengthUnits = 'm' | 'ft' | 'FL' | 'cm' | 'km' | 'mi' | 'NM'

function convertLength(
  values: [number | null, number | null],
  digits: number = 1,
  toUnit: LengthUnits = 'm',
  fromUnit: LengthUnits = 'm',
): string {
  const convertTable: Record<LengthUnits, number> = {
    cm: 0.01,
    FL: 30.48,
    ft: 0.3048,
    km: 1000,
    m: 1,
    mi: 1609.344,
    NM: 1852,
  }

  const [e, a] = values
  if (e === null) return 'N/A'

  const ne = (e * convertTable[fromUnit]) / convertTable[toUnit]
  if (a === null) return `${ne.toFixed(digits)} ${toUnit}`

  const na = (a * convertTable[fromUnit]) / convertTable[toUnit]
  return `${ne.toFixed(digits)} ± ${na.toFixed(digits)} ${toUnit}`
}

type TemperatureUnits = '°C' | '°F' | 'K'

function convertTemperature(
  value: number | null,
  digits: number = 1,
  toUnit: TemperatureUnits = '°C',
  fromUnit: TemperatureUnits = '°C',
): string {
  if (value === null) return 'N/A'
  const celsius = { '°C': value, '°F': (value - 32) / 1.8, K: value - 273.15 }[fromUnit]
  const target = { '°C': celsius, '°F': celsius * 1.8 + 32, K: celsius + 273.15 }[toUnit]
  return `${target.toFixed(digits)} ${toUnit}`
}

export {
  convertLength as convertLength,
  convertTemperature as convertTemperature,
  type LengthUnits as DistanceUnits,
  type TemperatureUnits,
}
