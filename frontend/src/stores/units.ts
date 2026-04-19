type DistanceUnits = 'm' | 'ft' | 'FL' | 'cm' | 'km' | 'mi' | 'NM'

function convertDistanceFromMeter(value: number | null, to: DistanceUnits): number | null {
  if (value === null) return null
  const 转换表: Map<DistanceUnits, number> = new Map([
    ['cm', 0.01],
    ['FL', 30.48],
    ['ft', 0.3048],
    ['km', 1000],
    ['m', 1],
    ['mi', 1609.344],
    ['NM', 1852],
  ])
  return value / 转换表.get(to)!
}

type TemperatureUnits = '°C' | '°F' | 'K'

function convertTemperatureFromCelsius(value: number | null, to: TemperatureUnits): number | null {
  return value ? { '°F': value * 1.8 + 32, '°C': value, K: value + 273.15 }[to] : value
}

export {
  convertDistanceFromMeter,
  convertTemperatureFromCelsius,
  type DistanceUnits,
  type TemperatureUnits,
}
