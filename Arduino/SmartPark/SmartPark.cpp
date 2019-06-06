#include "SmartPark.h"
#include "HardwareSerial.h"
#include "Arduino.h"
Sensor::Sensor(int pin) 
{
	_pin = pin;
	_analogValue = 0;
	_isCrossed = false;
	_threshold = 500;
}
Sensor::Sensor() 
{
	_pin = 0;
	_analogValue = 0;
	_isCrossed = false;
	_threshold = 500;
	_lastState = false;
}
void Sensor::sense()
{
 	_analogValue = analogRead(_pin);
	if(_crossCheck(_analogValue))
	{
		_isCrossed = true;
	}
	else
	{
		_isCrossed = false;
	}
}
void Sensor::stateChange()
{
	_lastState = !_lastState;
}
bool Sensor::getState()
{
	return _lastState;
}
bool Sensor::isSwitched()
{
	if(((_isCrossed)&&(!_lastState))||((!_isCrossed)&&(_lastState)))
	{
		return true;
	}
	return false;
}
bool Sensor::_crossCheck(int value)
{
	if (value < _threshold)
	{
		return true;
	}
	return false;
}
bool Sensor::isCrossed() 
{
	return _isCrossed;
}
int Sensor::getPin()
{
	return _pin;
}



Vehicle::Vehicle()
{
	vec minus_one;
	_lastPos = -1;
	_isFree = true;
	_spot = -1;
	_sequence.setLen(1);
	for(unsigned int i = 0; i < SENS_NUM; i++) 
	{
		minus_one.v[i] = -1;
	}
	_sequence.fill(minus_one);
}
int Vehicle::getNextPos() 
{
	vec sensors = _sequence.getList();
	for(int i = 0; i < _sequence.getLen(); i++) 
	{
		if (sensors.v[i] == _lastPos)
		{
			if(i == _sequence.getLen() - 1)
			{
				return -1;
			} else 
			{
				return sensors.v[i+1];
			}
		}
	}
}
void Vehicle::lastPosUpdate(int last_position)
{
	_lastPos = last_position;
}
int Vehicle::getLastPos()
{
	return _lastPos;
}
void Vehicle::assignSequence(vec seq)
{
	_sequence.fill(seq);
	_isFree = false;
}
void Vehicle::assignLength(int len)
{
	_sequence.setLen(len);
}
bool Vehicle::isFree()
{
	return _isFree;
}
void Vehicle::_isEnd()
{
	if(_sequence.getList().v[_sequence.getLen()-1] == _lastPos)
	{
		_isFree == true;
	}
}
void Vehicle::_setOccupied()
{
	_isFree = false;
}
void Vehicle::assignFromSeq(Sequence seq)
{
	_sequence = seq;
	_isFree = false;
}
void Vehicle::updateSpot(int spot) 
{
	_spot = spot;
}
void Vehicle::reset()
{
	vec minus_one;
	_lastPos = -1;
	_isFree = true;
	_spot = -1;
	for(unsigned int i = 0; i < SENS_NUM; i++) 
	{
		minus_one.v[i] = -1;
	}
	_sequence.setLen(1);
	_sequence.fill(minus_one);
}



Sequence::Sequence() 
{
	_length = 0;
	for(int i = 0; i < SENS_NUM; i++)
	{
		_sensors.v[i] = -1;
	}
}
vec Sequence::getList()
{
	return _sensors;
}
void Sequence::setLen(int len)
{
	_length = len;
}
Sequence::Sequence(int len)
{
	_length = len;
	for(int i = 0; i < len; i++) 
	{
		_sensors.v[i] = 0;
	}
	for(int i = len; i < SENS_NUM; i++)
	{
		_sensors.v[i] = -1;
	}
}
void Sequence::fill(vec sequence)
{
	for(int i = 0; i < _length; i++)
	{
		_sensors.v[i] = sequence.v[i];
	}
}
int Sequence::getLen()
{
	return _length;
}
int getlen(vec array)
{
	int i = 0;
	int cnt = 0;
	while(array.v[i] != -1)
	{
		i+=1;
	}
	return i;
}

