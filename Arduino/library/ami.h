#ifndef ami_h
#define ami_h

typedef struct 
{
	int v[12];
} vec;

class Sensor 
{
	public:
		Sensor(int pin);
		Sensor();
		bool isCrossed();
		void sense();
		int getPin();
	private:
		bool _crossCheck(int value);
		int _pin;
		int _analogValue;
		bool _isCrossed;
		int _threshold;
};
class Sequence
{
	public:
		Sequence();
		Sequence(int len);
		void fill(vec sequence);
		void setLen(int len);
		int getLen();
		vec getList();
	private:
		int _length;
		vec _sensors;
};

class Vehicle
{
	public:
		Vehicle();
		void assignSequence(vec seq);
		void assignFromSeq(Sequence seq);
		void assignLength(int len);
		void lastPosUpdate(int last_position);
		int getLastPos();
		int getNextPos();
		void updateSpot(int spot);
		bool isFree();
		
	private:
		void _setOccupied();
		void _clear();
		void _isEnd();
		int _lastPos;
		bool _isFree;
		Sequence _sequence;
};



int getlen(vec array);

#endif
