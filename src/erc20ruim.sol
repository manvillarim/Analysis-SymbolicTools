// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ERC20r {
    string public name = "MeuToken";
    string public symbol = "MTK";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    address public owner;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Mint(address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor(uint256 _initialSupply) {
        owner = msg.sender;
        totalSupply = _initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply; // Atribui o total de tokens ao criador do contrato
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Saldo insuficiente");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= balanceOf[_from], "Saldo insuficiente");
        require(_value <= allowance[_from][msg.sender]);
        
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }

    // Função Mint: cria novos tokens e os atribui ao endereço especificado
    function mint(address _to, uint256 _value) public onlyOwner returns (bool success) {
        totalSupply += _value * 10 ** uint256(decimals);
        balanceOf[_to] += _value * 10 ** uint256(decimals);
        emit Mint(_to, _value);
        emit Transfer(address(0), _to, _value);
        return true;
    }

    // Função Burn: queima tokens de um endereço específico
    function burn(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value, "Saldo insuficiente para queimar");
        
        balanceOf[_from] -= _value * 10 ** uint256(decimals);
        totalSupply -= _value * 10 ** uint256(decimals);
        
        emit Burn(_from, _value);
        emit Transfer(_from, address(0), _value);
        
        return true;
    }
}
